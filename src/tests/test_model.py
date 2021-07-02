from datetime import datetime

from hiperline.model import Scenario


def new_scenario(items, milestones, date_format):
    return Scenario(
        name="Scenario",
        items=items,
        milestones=milestones,
        start=datetime.strptime("1500-01-01", date_format),
        end=datetime.now(),
    )


def test_pretty(date_format, dpedro_I, dpedro_II, independencia, republica):
    scenario = new_scenario(
        items={dpedro_I, dpedro_II}, milestones={independencia, republica}, date_format=date_format
    )
    output = scenario.pretty()
    assert (
        output
        == "+--------------+----------------------------------------------+-----------------------------------------+\n"
        + "|              |     Independência do Brasil (07/09/1822)     |  Proclamação da República (15/11/1889)  |\n"
        + "+--------------+----------------------------------------------+-----------------------------------------+\n"
        + "| Dom Pedro I  |         Dom Pedro I tinha 23 ano(s)          | Dom Pedro I havia falecido há 55 ano(s) |\n"
        + "| Dom Pedro II | Faltava(m) 3 ano(s) para Dom Pedro II nascer |       Dom Pedro II tinha 63 ano(s)      |\n"
        + "+--------------+----------------------------------------------+-----------------------------------------+"
    )


def test_alive_during_milestone(date_format, dpedro_I, independencia):
    scenario = new_scenario(items={dpedro_I}, milestones={independencia}, date_format=date_format)
    table = scenario.generate()
    assert table[0][1] == "Independência do Brasil (07/09/1822)"
    assert table[1][0] == "Dom Pedro I"
    assert table[1][1] == "Dom Pedro I tinha 23 ano(s)"


def test_dead_before_milestone(date_format, dpedro_I, republica):
    scenario = new_scenario(items={dpedro_I}, milestones={republica}, date_format=date_format)
    table = scenario.generate()
    assert table[0][1] == "Proclamação da República (15/11/1889)"
    assert table[1][0] == "Dom Pedro I"
    assert table[1][1] == "Dom Pedro I havia falecido há 55 ano(s)"


def test_born_after_milestone(date_format, dpedro_II, independencia):
    scenario = new_scenario(items={dpedro_II}, milestones={independencia}, date_format=date_format)
    table = scenario.generate()
    assert table[0][1] == "Independência do Brasil (07/09/1822)"
    assert table[1][0] == "Dom Pedro II"
    assert table[1][1] == "Faltava(m) 3 ano(s) para Dom Pedro II nascer"


def test_item_is_milestone(date_format, dpedro_II):
    scenario = new_scenario(items={dpedro_II}, milestones={dpedro_II}, date_format=date_format)
    table = scenario.generate()
    assert table[0][1] == "Dom Pedro II (02/12/1825)"
    assert table[1][0] == "Dom Pedro II"
    assert table[1][1] == "Faltava(m) 0 ano(s) para Dom Pedro II nascer"


def test_printing(date_format, dpedro_I, republica):
    scenario = new_scenario(items={dpedro_I}, milestones={republica}, date_format=date_format)
    table = scenario.generate()
    assert table[0][1] == "Proclamação da República (15/11/1889)"
    assert table[1][0] == "Dom Pedro I"
    assert table[1][1] == "Dom Pedro I havia falecido há 55 ano(s)"
