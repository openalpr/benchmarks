from moealpr.alpr_experiment import AlprExperiment
from moealpr.alpr_setting import AlprConfigSetting, SettingType
from moealpr.alpr_benchmark import AlprEndToEndBenchmark

settings = [
    AlprConfigSetting('segmentation_min_box_width_px', 0, 12, 4, setting_type=SettingType.INTEGER),
    AlprConfigSetting('segmentation_min_charheight_percent', 0, 1.0, 0.5),
    AlprConfigSetting('segmentation_max_segment_width_percent_vs_average', 0, 3.0, 1.35)
    ]

benchmark = AlprEndToEndBenchmark()

experiment = AlprExperiment(benchmark, settings)

experiment.run(200)