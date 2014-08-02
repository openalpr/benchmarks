from moealpr.alpr_experiment import AlprExperiment
from moealpr.alpr_setting import AlprConfigSetting
from moealpr.alpr_benchmark import AlprEndToEndBenchmark

settings = [
    AlprConfigSetting('postprocess_min_confidence', 0, 100, 65),
    AlprConfigSetting('postprocess_confidence_skip_level', 0, 100, 80)
    ]

benchmark = AlprEndToEndBenchmark()

experiment = AlprExperiment(benchmark, settings)

experiment.run(200)