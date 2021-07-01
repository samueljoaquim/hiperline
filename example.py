from datetime import datetime

from model import Person, Scenario, Milestone


date_format = "%Y-%m-%d"

dpedro_I = Person(
    name="Dom Pedro I",
    start=datetime.strptime("1798-10-12", date_format),
    end=datetime.strptime("1834-09-24", date_format)
)

descobrimento = Milestone(
    name="Descobrimento do Brasil",
    start=datetime.strptime("1500-04-22", date_format)
)

independencia = Milestone(
    name="Independência do Brasil",
    start=datetime.strptime("1822-09-07", date_format)
)

scenario = Scenario(
    name="Brasil",
    items={dpedro_I, },
    milestones={descobrimento, independencia},
    start=datetime.strptime("1500-04-22", date_format),
    end=datetime.now()
)
