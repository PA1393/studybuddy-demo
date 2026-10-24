import React from "react";

export interface Student {
  id: string;
  name: string;
  grade: number;
  subjects: string[];
  avatarUrl: string;
}

interface ProfileCardProps {
  student: Student;
  onSelect?: (id: string) => void;
}

export function ProfileCard({ student, onSelect }: ProfileCardProps) {
  return (
    <div className="profile-card">
      <img src={student.avatarUrl} />
      <h3>{student.name}</h3>
      <p>Grade {student.grade}</p>
    </div>
  );
}
