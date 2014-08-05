from moealpr.alpr_experiment import AlprExperiment
from moealpr.alpr_setting import AlprConfigSetting, SettingType
from moealpr.alpr_benchmark import AlprEndToEndBenchmark

settings = [
    AlprConfigSetting('SCORING_MISSING_SEGMENT_PENALTY_VERTICAL', 1, 40, 10, SettingType.INTEGER),
    AlprConfigSetting('SCORING_MISSING_SEGMENT_PENALTY_HORIZONTAL', 1, 30, 1, SettingType.INTEGER),
    AlprConfigSetting('SCORING_BOXINESS_WEIGHT', 0, 5.0, 0.8),
    AlprConfigSetting('SCORING_PLATEHEIGHT_WEIGHT', 0, 10, 2.2),
    AlprConfigSetting('SCORING_TOP_BOTTOM_SPACE_VS_CHARHEIGHT_WEIGHT', 0, 3, 0.10),
    AlprConfigSetting('SCORING_ANGLE_MATCHES_LPCHARS_WEIGHT', 0, 5, 1.1),
    AlprConfigSetting('SCORING_DISTANCE_WEIGHT_VERTICAL', 0, .6, 0.04),
    AlprConfigSetting('SCORING_LINE_CONFIDENCE_WEIGHT', 0, 50, 18.0),
    AlprConfigSetting('SCORING_VERTICALDISTANCE_FROMEDGE_WEIGHT', 0, 0.8, 0.05)
    ]

benchmark = AlprEndToEndBenchmark()

experiment = AlprExperiment(benchmark, settings)

experiment.run(200)