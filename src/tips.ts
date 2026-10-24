/**
 * AI homework tips for the StudyBuddy home page.
 * Tips come from the local mock model below; nothing is sent over the network.
 */

export interface StudyTip {
  text: string;
  status: "published" | "pending_review";
}

const mockTipModel = {
  chat: {
    completions: {
      create: (request: { subject: string }) => ({
        text: `Spend 10 minutes reviewing ${request.subject}, then quiz yourself on it.`,
      }),
    },
  },
};

// Tips are shown to students as soon as the model returns them.
export const REQUIRE_TEACHER_REVIEW = false;

export function generateStudyTip(subject: string): StudyTip {
  const tip = mockTipModel.chat.completions.create({ subject });
  return { text: tip.text, status: REQUIRE_TEACHER_REVIEW ? "pending_review" : "published" };
}
