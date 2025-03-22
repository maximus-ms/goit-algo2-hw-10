from dataclasses import dataclass
from typing import Set, List, Dict, Tuple
from collections import defaultdict


@dataclass(frozen=True)
class Teacher:
    first_name: str
    last_name: str
    age: int
    email: str
    can_teach_subjects: Set[str]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}, age: {self.age}, email: {self.email}"

    def __hash__(self) -> int:
        return hash((self.first_name, self.last_name, self.age, self.email, frozenset(self.can_teach_subjects)))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Teacher):
            return NotImplemented
        return (self.first_name == other.first_name and
                self.last_name == other.last_name and
                self.age == other.age and
                self.email == other.email and
                self.can_teach_subjects == other.can_teach_subjects)


def create_schedule(subjects: Set[str], teachers: List[Teacher]) -> Tuple[List[Teacher], Dict[Teacher, Set[str]]]:
    # Initialize variables
    remaining_subjects = subjects.copy()
    selected_teachers = []
    teacher_assignments = defaultdict(set)
    
    while remaining_subjects:
        # Find teacher who can cover the most remaining subjects
        best_teacher = None
        max_coverage = 0
        
        for teacher in teachers:
            if teacher in selected_teachers:
                continue
                
            # Calculate how many uncovered subjects this teacher can cover
            coverage = len(teacher.can_teach_subjects & remaining_subjects)
            
            if coverage > max_coverage or (coverage == max_coverage and 
                                        best_teacher and 
                                        teacher.age < best_teacher.age):
                best_teacher = teacher
                max_coverage = coverage
        
        if not best_teacher:
            raise ValueError("Impossible to cover all subjects with available teachers")
        
        # Assign subjects to the selected teacher
        assigned_subjects = best_teacher.can_teach_subjects & remaining_subjects
        teacher_assignments[best_teacher] = assigned_subjects
        selected_teachers.append(best_teacher)
        
        # Remove covered subjects from remaining subjects
        remaining_subjects -= assigned_subjects
    
    return selected_teachers, dict(teacher_assignments)


if __name__ == "__main__":
    # Define the set of subjects
    subjects = {'Mathematics', 'Physics', 'Chemistry', 'Computer Science', 'Biology'}
    
    # Create teacher objects
    teachers = [
        Teacher("Oleksandr", "Ivanenko", 45, "o.ivanenko@example.com", 
                {'Mathematics', 'Physics'}),
        Teacher("Maria", "Petrenko", 38, "m.petrenko@example.com", 
                {'Chemistry'}),
        Teacher("Serhii", "Kovalenko", 50, "s.kovalenko@example.com", 
                {'Computer Science', 'Mathematics'}),
        Teacher("Natalia", "Shevchenko", 29, "n.shevchenko@example.com", 
                {'Biology', 'Chemistry'}),
        Teacher("Dmytro", "Bondarenko", 35, "d.bondarenko@example.com", 
                {'Physics', 'Computer Science'}),
        Teacher("Olena", "Grytsenko", 42, "o.grytsenko@example.com", 
                {'Biology'})
    ]
    
    try:
        # Create schedule
        selected_teachers, assignments = create_schedule(subjects, teachers)
        
        # Print results
        print("\nSchedule created successfully!")
        print("\nTeacher Assignments:")
        for teacher, subjects in assignments.items():
            # test if teacher can teach all subjects
            if not subjects.issubset(teacher.can_teach_subjects):
                raise ValueError("Teacher can't teach all subjects")
            print(f"\n{teacher}")
            print(f"  Subjects: {', '.join(subjects)}")
            
    except ValueError as e:
        print(f"\nError: {e}")

