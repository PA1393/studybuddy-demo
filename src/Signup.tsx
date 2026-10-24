import React, { useState } from "react";

/**
 * StudyBuddy Registration Component
 * Allows students to register for peer tutoring and study partner matching.
 */

interface SignupProps {
  onSuccess?: () => void;
  defaultEmail?: string;
}

export function Signup({ onSuccess, defaultEmail = "" }: SignupProps) {
  const [email, setEmail] = useState(defaultEmail);
  const [birthYear, setBirthYear] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) {
      setError("Email required");
      return;
    }
    setSubmitted(true);
    onSuccess?.();
  };

  return (
    <div className="signup-container">
      <h2>Join StudyBuddy</h2>
      <p>Find peer study partners for high school classes.</p>
      {/* Registration Form */}
      <form onSubmit={handleSubmit} className="signup-form">
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your student email"
        />
        <input
          type="text"
          value={birthYear}
          onChange={(e) => setBirthYear(e.target.value)}
          placeholder="Birth year (e.g. 2008)"
        />
        <button type="submit" className="button-primary">
          Create Free Account
        </button>
      </form>
    </div>
  );
}
