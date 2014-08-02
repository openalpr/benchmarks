from moealpr.alpr_experiment import AlprExperiment
from moealpr.alpr_setting import AlprConfigSetting, SettingType
from moealpr.alpr_benchmark import AlprEndToEndBenchmark

settings = [
    AlprConfigSetting('char_analysis_min_pct', 0.01, 1, .30),
    AlprConfigSetting('char_analysis_height_range', 0.01, 1, .20),
    AlprConfigSetting('char_analysis_height_step_size', 0.01, 1, .10),
    AlprConfigSetting('char_analysis_height_num_steps', 1, 5, 4, setting_type=SettingType.INTEGER)
    ]

benchmark = AlprEndToEndBenchmark()

experiment = AlprExperiment(benchmark, settings)

experiment.run(400)