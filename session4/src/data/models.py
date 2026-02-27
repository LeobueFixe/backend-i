from dataclasses import dataclass

@dataclass
class Meeting:
    title: str
    owner: str
    date: str

    def __str__(self):
        return (
            "| Field | Value |\n"
            "|-------|--------|\n"
            f"| Title | {self.title} |\n"
            f"| Owner | {self.owner} |\n"
            f"| Date  | {self.date} |\n"
            "\n# Meeting\n"
        )

    