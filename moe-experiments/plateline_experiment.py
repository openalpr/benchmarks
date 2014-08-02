from moealpr.alpr_experiment import AlprExperiment
from moealpr.alpr_setting import AlprConfigSetting, SettingType
from moealpr.alpr_benchmark import AlprEndToEndBenchmark

settings = [
    AlprConfigSetting('plateline_sensitivity_vertical', 1, 100, 25, SettingType.INTEGER),
    AlprConfigSetting('plateline_sensitivity_horizontal', 1, 100, 45, SettingType.INTEGER)
    ]

benchmark = AlprEndToEndBenchmark()

experiment = AlprExperiment(benchmark, settings)

experiment.run(200)