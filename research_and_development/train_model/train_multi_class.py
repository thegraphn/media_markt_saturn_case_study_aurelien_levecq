# fmt: off
import logging
from pathlib import Path

from farm.data_handler.data_silo import DataSilo
from farm.data_handler.processor import TextClassificationProcessor
from farm.modeling.optimization import initialize_optimizer
from farm.infer import Inferencer
from farm.modeling.adaptive_model import AdaptiveModel
from farm.modeling.language_model import LanguageModel
from farm.modeling.prediction_head import TextClassificationHead
from farm.modeling.tokenization import Tokenizer
from farm.train import Trainer, EarlyStopping
from farm.utils import set_all_seeds, MLFlowLogger, initialize_device_settings


def doc_classification_multilabel():
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO)

    ml_logger = MLFlowLogger(tracking_uri="https://public-mlflow.deepset.ai/")
    ml_logger.init_experiment(experiment_name="categories_articles_one_label", run_name="3")
    ##########################
    ########## Settings
    ##########################
    set_all_seeds(seed=42)
    device, n_gpu = initialize_device_settings(use_cuda=True)
    n_epochs = 30
    batch_size = 6

    evaluate_every = 51
    lang_model = "bert-base-german-cased"
    do_lower_case = False

    # 1.Create a tokenizer
    tokenizer = Tokenizer.load(
        pretrained_model_name_or_path=lang_model,
        do_lower_case=do_lower_case)

    label_list = ['257', '231', '788', '237', '293', '224', '307', '750', '295', '784', '252', '310', '266', '286',
                  '324', '342', '298', '226', '305', '207', '249', '326', '331', '8022', '225', '255', '253', '749',
                  '296', '325', '303', '316', '308', '261', '291', '322', '282', '312', '332', '220', '297', '299',
                  '269', '279', '233', '223', '319', '284', '235', '210', '314', '263', '238', '315', '4561', '259',
                  '208', '265', '262']

    metric = "f1_macro"
    processor = TextClassificationProcessor(tokenizer=tokenizer,
                                            max_seq_len=512,
                                            data_dir=Path("../../data/training_data"),
                                            label_list=label_list,
                                            metric=metric,
                                            quote_char='"',
                                            multilabel=False,
                                            train_filename="train_one_label.csv",
                                            test_filename="test_one_label.csv",
                                            dev_split=0.2,
                                            delimiter="\t",

                                            )

    # 3. Create a DataSilo that loads several datasets (train/dev/test), provides DataLoaders for them and calculates a few descriptive statistics of our datasets
    data_silo = DataSilo(
        processor=processor,
        batch_size=batch_size)

    # 4. Create an AdaptiveModel
    # a) which consists of a pretrained language model as a basis
    language_model = LanguageModel.load(lang_model)
    # b) and a prediction head on top that is suited for our task => Text classification
    prediction_head = TextClassificationHead(num_labels=len(label_list))

    model = AdaptiveModel(
        language_model=language_model,
        prediction_heads=[prediction_head],
        embeds_dropout_prob=0.1,
        lm_output_types=["per_sequence"],
        device=device)

    # 5. Create an optimizer
    model, optimizer, lr_schedule = initialize_optimizer(
        model=model,
        learning_rate=3e-5,
        device=device,
        n_batches=len(data_silo.loaders["train"]),
        n_epochs=n_epochs)
    save_dir = Path(
        "/home/graphn/PycharmProjects/media_markt_saturn_case_study_aurelien_levecq/research_and_development/trained_model/category_one_label")

    earlystopping = EarlyStopping(
        metric="f1_macro", mode="max",
        save_dir=save_dir,  # where to save the best model
        patience=round(n_epochs * 0.3)  # number of evaluations to wait for improvement before terminating the training
    )

    # 6. Feed everything to the Trainer, which keeps care of growing our model into powerful plant and evaluates it from time to time
    trainer = Trainer(
        model=model,
        optimizer=optimizer,
        data_silo=data_silo,
        epochs=n_epochs,
        n_gpu=n_gpu,
        lr_schedule=lr_schedule,
        evaluate_every=evaluate_every,
        device=device,
        early_stopping=earlystopping
    )

    # 7. Let it grow
    trainer.train()

    # 9. Load it & harvest your fruits (Inference)
    basic_texts = [
        {"text": "1254390 KDL 40 WE 5 BAEP SCHWARZ[SEP]"},
        {"text": "1788154 AZ 105 S/12[SEP]"},
    ]
    model = Inferencer.load(save_dir, gpu=True)
    result = model.inference_from_dicts(dicts=basic_texts)
    for batch in result:
        print(batch)
        for x in batch["predictions"]:
            pred = x["label"]
            print(pred)

    model.close_multiprocessing_pool()
    print(sorted(label_list))


if __name__ == "__main__":
    doc_classification_multilabel()

# fmt: on
