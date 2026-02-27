from domains.models import Meeting

meetings = MeetingManager()

meeting1 = Meeting("1", "Aula da tarde", "27/02/2026", "Jorge", ["Zé+", "António Cabral"], ["Sim é bunito", "Leo", "DATE", "open"])
meeting2 = Meeting("2", "Aula da manhã", "29/02/2026", "Jorge", ["BUU", "BOID"], ["Não", "Dino", "DATE", "open"])
meetings.add(meeting1, meeting2)