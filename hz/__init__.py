from .ich_representative_project import main as ich_representative_project_main
from .test import main as test_main

__all__ = ["start_transform_hz_data"]


def start_transform_hz_data():
    # 非物质文化遗产
    ich_representative_project_main()

    # 测试
    # test_main()