from typing import Dict, List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from actions.action import Action


class Skillset:

    def __init__(self,
                 all_skills: Dict[str, List["Action"]],
                 primary_job: str,
                 secondary_job: Optional[str],
                 passive: Optional[str]):
        """
        A dataclass that stores the Adventurer/Monster's primary skillset, secondary skillset,
        and passive skillset.

        Inputs:
            - all_skills: a dictionary containing the list of spells and abilities the adventurer
                knows in each class.
            - primary_job (str): the job name representing their primary job. This is ALWAYS their
                current job.
            - secondary_job (str): the job name representing their secondary job.
            - passive (str): the name of the ability they have "equipped" as their passive.

        Attributes:
            - Primary skillset (List[Action]): the primary skillset. This is ALWAYS the skillset
                of whatever job they currently have.
            - Secondary spellset (List[Action]): the secondary skillset. This can be chosen among
                all skillsets of different jobs the adventurer possesses.
            - Passive: Not Implemented.
        """
        self._all_skills = all_skills
        self._primary_skillset = self._all_skills[primary_job]
        self._secondary_skillset = self._all_skills[secondary_job]
        self._passive = passive

    @property
    def primary_skillset(self) -> List["Action"]:
        return self._primary_skillset
    
    @property
    def secondary_skillset(self) -> List["Action"]:
        return self._secondary_skillset
    
    def set_secondary_job(self, job_name: str) -> None:
        """Set secondary job to the job named job_name."""
        self._secondary_skillset = self._all_skills[job_name]
    
    def set_passive(self, passive_name: "Action") -> None:
        """Set passive to the Action named passive_name."""
        self._passive = passive_name

    def add_skill(self, skill: "Action", job_name: str) -> None:
        """Add skill to the skillset corresponding to job_name."""
        if skill not in self._all_skills[job_name]:
            self._all_skills[job_name].append(skill)