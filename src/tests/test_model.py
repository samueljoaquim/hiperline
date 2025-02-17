from datetime import datetime

from hiperline.model import PointInTime, Scenario


def new_scenario(items, milestones):
    return Scenario(
        name="Scenario",
        items=items,
        milestones=milestones,
        start=datetime(1500, 1, 1),
        end=datetime.now(),
    )


def test_pretty(portuguese, dpedro_I, dpedro_II, independencia, republica):
    scenario = new_scenario(items={dpedro_I, dpedro_II}, milestones={independencia, republica})
    output = scenario.pretty(language=portuguese)
    assert (
        output
        == "+--------------+----------------------------------------------+-----------------------------------------+\n"
        + "|              |     Independência do Brasil (07/09/1822)     |  Proclamação da República (15/11/1889)  |\n"
        + "+--------------+----------------------------------------------+-----------------------------------------+\n"
        + "| Dom Pedro I  |         Dom Pedro I tinha 23 ano(s)          | Dom Pedro I havia falecido há 55 ano(s) |\n"
        + "| Dom Pedro II | Faltava(m) 3 ano(s) para Dom Pedro II nascer |       Dom Pedro II tinha 63 ano(s)      |\n"
        + "+--------------+----------------------------------------------+-----------------------------------------+"
    )


def test_alive_during_milestone(dpedro_I, independencia):
    scenario = new_scenario(items={dpedro_I}, milestones={independencia})
    table = scenario.generate_events()
    assert table[0][1] == "Independência do Brasil (07/09/1822)"
    assert table[1][0] == ("Dom Pedro I", PointInTime.WAS_HAPPENING, 23)


def test_text_alive_during_milestone(portuguese, dpedro_I, independencia):
    scenario = new_scenario(items={dpedro_I}, milestones={independencia})
    table = scenario.generate(language=portuguese)
    assert table[0][1] == "Independência do Brasil (07/09/1822)"
    assert table[1][0] == "Dom Pedro I"
    assert table[1][1] == "Dom Pedro I tinha 23 ano(s)"


def test_dead_before_milestone(dpedro_I, republica):
    scenario = new_scenario(items={dpedro_I}, milestones={republica})
    table = scenario.generate_events()
    assert table[0][1] == "Proclamação da República (15/11/1889)"
    assert table[1][0] == ("Dom Pedro I", PointInTime.ENDED_BEFORE, 55)


def test_text_dead_before_milestone(portuguese, dpedro_I, republica):
    scenario = new_scenario(items={dpedro_I}, milestones={republica})
    table = scenario.generate(language=portuguese)
    assert table[0][1] == "Proclamação da República (15/11/1889)"
    assert table[1][0] == "Dom Pedro I"
    assert table[1][1] == "Dom Pedro I havia falecido há 55 ano(s)"


def test_born_after_milestone(dpedro_II, independencia):
    scenario = new_scenario(items={dpedro_II}, milestones={independencia})
    table = scenario.generate_events()
    assert table[0][1] == "Independência do Brasil (07/09/1822)"
    assert table[1][0] == ("Dom Pedro II", PointInTime.STARTED_AFTER, 3)


def test_text_born_after_milestone(portuguese, dpedro_II, independencia):
    scenario = new_scenario(items={dpedro_II}, milestones={independencia})
    table = scenario.generate(language=portuguese)
    assert table[0][1] == "Independência do Brasil (07/09/1822)"
    assert table[1][0] == "Dom Pedro II"
    assert table[1][1] == "Faltava(m) 3 ano(s) para Dom Pedro II nascer"


def test_item_is_milestone(dpedro_II):
    scenario = new_scenario(items={dpedro_II}, milestones={dpedro_II})
    table = scenario.generate_events()
    assert table[0][1] == "Dom Pedro II (02/12/1825)"
    assert table[1][0] == ("Dom Pedro II", PointInTime.STARTED_AFTER, 0)


def test_text_item_is_milestone(portuguese, dpedro_II):
    scenario = new_scenario(items={dpedro_II}, milestones={dpedro_II})
    table = scenario.generate(language=portuguese)
    assert table[0][1] == "Dom Pedro II (02/12/1825)"
    assert table[1][0] == "Dom Pedro II"
    assert table[1][1] == "Faltava(m) 0 ano(s) para Dom Pedro II nascer"


def test_printing(portuguese, dpedro_I, republica):
    scenario = new_scenario(items={dpedro_I}, milestones={republica})
    table = scenario.generate(language=portuguese)
    assert table[0][1] == "Proclamação da República (15/11/1889)"
    assert table[1][0] == "Dom Pedro I"
    assert table[1][1] == "Dom Pedro I havia falecido há 55 ano(s)"
