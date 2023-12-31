import datetime
import time
from typing import Any, Dict, Optional, Union

import pytorch_lightning as pl
from pytorch_lightning.callbacks.progress.rich_progress import RichProgressBar, RichProgressBarTheme


class RichDefaultThemeProgressBar(RichProgressBar):

    def __init__(
            self,
            refresh_rate: int = 1,
            leave: bool = False,
            console_kwargs: Optional[Dict[str, Any]] = None,
            show_version: Optional[bool] = False,
            show_eta_time: Optional[bool] = False,
    ) -> None:
        super().__init__(refresh_rate = refresh_rate, leave = leave, theme = RichProgressBarTheme(), console_kwargs = console_kwargs)
        self.show_version = show_version
        self.show_eta_time = show_eta_time

    def on_train_start(self, trainer, pl_module):
        super().on_train_start(trainer, pl_module)
        if self.show_eta_time:
            self.start_time = time.time()
            self.start_epoch = trainer.current_epoch

    def get_metrics(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> Dict[str, Union[int, str]]:
        items = super().get_metrics(trainer, pl_module)
        if not self.show_version:
            # don't show the version number
            items.pop("v_num", None)
        if self.show_eta_time and self.trainer.training and self.trainer.max_epochs is not None and self.trainer.max_epochs < 1000:
            during_time = time.time() - self.start_time
            time_sec_avg = during_time / ((self.trainer.current_epoch - self.start_epoch) * self.total_train_batches + self.train_batch_idx)
            eta_time = time_sec_avg * (
                    (self.trainer.max_epochs - self.trainer.current_epoch) * self.total_train_batches - self.train_batch_idx)
            items['ETA'] = str(datetime.timedelta(seconds = int(eta_time)))
        return items
