from domains.models import Meeting, MeetingManager
from uuid import uuid4

meetings = MeetingManager()

meeting1 = Meeting(str(uuid4()), "Aula da tarde", "27/02/2026", "Jorge", ["Zé+", "António Cabral"], ["Sim é bunito", "Leo", "DATE", "open"])
meeting2 = Meeting(str(uuid4()), "Aula da manhã", "29/02/2026", "Jorge", ["BUU", "BOID"], ["Não", "Dino", "DATE", "open"])
meetings.add(meeting1, meeting2)