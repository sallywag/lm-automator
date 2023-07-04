import argparse

import yaml

from lm_automator.layout_manager import LayoutManager
from lm_automator.page import Page
from lm_automator.layout_manager_factory import LayoutManagerFactory


def generate() -> None:
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--flow_file", dest="flow_file", action="store", required=True)
    parser.add_argument("--config_file", dest="config_file", action="store", required=True)
    parser.add_argument("--model_file", dest="model_file", action="store", required=True)

    with open(parser.parse_args().flow_file, "r") as file:
        flow_data = yaml.safe_load(file)
    with open(parser.parse_args().config_file, "r") as file:
        config_data = yaml.safe_load(file)
    with open(parser.parse_args().model_file, "r") as file:
        model_data = yaml.safe_load(file)

    layout_manager = LayoutManager(config_data["environment"], flow_data["site"])
    layout_manager.login(config_data["username"], config_data["password"])

    factory = LayoutManagerFactory(model_data)

    for test in flow_data["tests"]:
        Page.visit(test["page"])
        if test.get("layout"):
            Page.select_layout(test["layout"])

        for step in test["steps"]:
            if step["action"] == "add-components":
                flow_data.get_region(step["region"], test["page"]).add_components(
                    (step["components"])
                )
            elif step["action"] == "edit-component":
                component = flow_data.get_component(step["region"], step["index"])
                component.edit()
                for action in step["steps"]:
                    input_ = flow_data.get_input(
                        step["region"], step["component"], action["input"]
                    )
                    if action["action"] == "click":
                        input_.click()
                    elif action["action"] == "select":
                        input_.option = action["value"]
                    elif action["action"] == "check":
                        input_.checked = action["value"]
                    elif action["action"] == "set":
                        input_.value = action["value"]
                component.edit()
            elif step["action"] == "remove-component":
                component = factory.get_component(step["region"], step["index"])
                component.delete()
