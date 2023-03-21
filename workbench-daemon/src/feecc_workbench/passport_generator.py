import datetime as dt
import pathlib
from typing import Any

import yaml
from loguru import logger

from .ProductionStage import ProductionStage
from .Unit import Unit


def _construct_stage_dict(prod_stage: ProductionStage) -> dict[str, Any]:
    stage: dict[str, Any] = {
        "Name": prod_stage.name,
        "Employee Code": prod_stage.employee_name,
        "Start Time": prod_stage.session_start_time,
        "Finish Time": prod_stage.session_end_time,
    }

    if prod_stage.prod_data_hashes is not None:
        stage["Assembly data in IPFS"] = prod_stage.prod_data_hashes

    if prod_stage.additional_info:
        stage["Additional Information"] = prod_stage.additional_info

    return stage


def _get_total_assembly_time(unit: Unit) -> dt.timedelta:
    """Calculate total assembly time of the unit and all its components recursively"""
    own_time: dt.timedelta = unit.total_assembly_time

    for component in unit.components_units:
        component_time = _get_total_assembly_time(component)
        own_time += component_time

    return own_time


def _get_passport_dict(unit: Unit) -> dict[str, Any]:
    """
    form a nested dictionary containing all the unit
    data to dump it into a human friendly passport
    """
    passport_dict: dict[str, Any] = {
        "Unit Unique Code": unit.uuid,
        "Unit Model Name": unit.model_name,
    }

    try:
        passport_dict["Total Assembly Time"] = str(unit.total_assembly_time)
    except Exception as e:
        logger.error(str(e))

    if unit.biography:
        passport_dict["Production Stages"] = [_construct_stage_dict(stage) for stage in unit.biography]

    if unit.components_units:
        passport_dict["Unit Components"] = [_get_passport_dict(c) for c in unit.components_units]
        passport_dict["Total Assembly Time (Including Components)"] = str(_get_total_assembly_time(unit))

    if unit.serial_number:
        passport_dict["Unit Serial Number"] = unit.serial_number

    return passport_dict


def _save_passport(unit: Unit, passport_dict: dict[str, Any], path: str) -> None:
    """makes a unit passport and dumps it in a form of a YAML file"""
    dir_ = pathlib.Path("unit-passports")
    if not dir_.is_dir():
        dir_.mkdir()
    passport_file = pathlib.Path(path)
    with passport_file.open("w") as f:
        yaml.dump(passport_dict, f, allow_unicode=True, sort_keys=False)
    logger.info(f"Unit passport with UUID {unit.uuid} has been dumped successfully")


@logger.catch(reraise=True)
async def construct_unit_passport(unit: Unit) -> pathlib.Path:
    """construct own passport, dump it as .yaml file and return a path to it"""
    passport = _get_passport_dict(unit)
    path = f"unit-passports/unit-passport-{unit.uuid}.yaml"
    _save_passport(unit, passport, path)
    return pathlib.Path(path)
