# 14 — Build the explanation one useful layer at a time

*Simplify complex ideas by layering*

You know how the system works, so you begin where its implementation begins. You describe the components, the queue, the transformation and the retry behavior. The listener interrupts: “Sorry—what problem does this solve?”

You have supplied accurate pieces before supplying the relationship that makes those pieces useful.

A layered explanation starts from the listener's question, establishes a workable picture and adds the detail needed for the next question. It is not an expert explanation with the difficult words removed. It is an explanation with a deliberate order of understanding.

## The principle: each layer should make the next one intelligible

Consider the difference between naming a component and explaining its job. “There is an approval queue” names something. “Requests wait here until an authorized reviewer checks them” establishes a function. Once that function is understood, you can explain who reviews, what gets checked and what happens when nobody responds.

The order depends on the listener. An experienced reviewer may already know the function and need only the exception rules. A new colleague may need to follow one request before the diagram means anything. Neither person needs to be treated as less capable. They need different starting points.

Layering is also different from merely shortening. Compression chooses how much to include. Layering chooses the dependencies among what you include: which idea must be understood before another one becomes useful?

## The source example: a course becomes an instrument and a composition

In *How to Explain Anything To Anyone*, Vinh Giang introduces his CLEAR filter: calibrate, link, envision, abstraction and repeat. He begins with checking what the audience knows, explicitly warning against both assuming too much and talking down to people.

One example contrasts a detailed description of his communication workshop with a music analogy. In his revised pitch, the first day concerns learning the instrument—voice and body language—and the second concerns composing the message. The detailed syllabus remains available separately.

That example makes two useful moves. It gives the listener an organizing distinction, and it does not require the short explanation to carry the entire curriculum. But the analogy does not tell a buyer everything needed to assess the course. Content, practice format and suitability still need explanation when those are the questions at hand.

Later, he explains stages of learning with plainer language and describes drawing a model, then returns to the framework at the end. We can inspect those verbal choices in the transcript; we cannot independently assess the unseen diagram from that text alone. Our layered method draws on calibration, linking and returning to the overall picture without presenting it as Vinh's exact named sequence.

## A worked application: explain an approval queue

*This workplace system is an invented teaching example, not documentation for a real product.*

A request system lets employees submit purchases. An authorized reviewer approves or rejects each request before an order is placed. Requests above a specified threshold need a second reviewer. The system sends a reminder when a request waits too long; it does not automatically approve it.

An implementation-first explanation:

> “The submission creates a pending record, and then the approval workflow routes it according to the configured threshold with a reminder event for unprocessed items.”

For someone who understands the components, this may be adequate. For a new requester, start elsewhere.

The first layer establishes the job:

> “Submitting the form asks for permission to buy something. It does not place the order. A reviewer needs to approve it first.”

The second follows one case:

> “Suppose you request a new monitor. The request waits for the designated reviewer. If it is approved, the order can proceed. If it is rejected, you receive the decision rather than an order confirmation.”

The third adds a branch:

> “Larger requests need a second approval. That is why two otherwise similar requests can have different waiting times.”

The fourth addresses a likely misunderstanding:

> “If the request waits too long, the system sends a reminder. Waiting does not turn a pending request into an approved one.”

Now return to the practical takeaway:

> “Before expecting an order, check that the request is approved—not merely submitted.”

Each layer answers a different question. The explanation is longer than the original sentence, but it provides the relationships a newcomer needs to act correctly.

## Use analogies with an exit

An analogy can establish a first picture, but its familiar features can also suggest things that are not true. Calling the queue a waiting room might help explain waiting; it might also imply that requests are handled strictly in arrival order. If that is not true, say so.

Name what the comparison explains and where it stops. “Like a waiting room, this is where requests wait for attention. Unlike a simple line, the reviewer may handle urgent requests first.” In a real system, use that qualification only if it accurately describes its rules.

You can often skip the analogy and use a concrete case instead. A purchase request moving through the actual stages may be more useful than a clever comparison. Familiarity is helpful only when it supports the right understanding.

## Check the next action, not just the nod

“Does that make sense?” is easy to answer politely. A more useful check fits the listener's task: “If the status says submitted, would you expect the order to have been placed?” Their answer tells you whether the crucial distinction landed.

Present the check as feedback on your explanation, not an examination of the listener. “Let me check that I've made the status difference clear” puts responsibility in the right place.

If they already understand the basics, move on. Asking someone to sit through every layer merely because you prepared it is another form of failing to calibrate.

## When this goes wrong

One failure is false simplicity: remove exceptions that change the listener's action. If some requests require a second approval, that condition belongs somewhere the relevant users will encounter it. A simple first layer should not become a false final account.

Another is the endless staircase. Every explanation reveals another prerequisite until the original question disappears. Return to the listener's task and ask which detail is needed for it. Not every architecture lesson belongs in an onboarding conversation.

A third is vocabulary substitution without conceptual explanation. Replacing “asynchronous” with “not at the same time” may not explain what the listener should expect. Say what happens and what they need to do.

Finally, avoid treating jargon as inherently bad. Shared technical language can be efficient among people who understand it. The problem is an unexplained dependency, not the mere presence of a specialist word.

## Practice: start with one case, then test an exception

Choose a process you explain regularly. Write its purpose, one ordinary case, one important exception and the action the listener should take. Order these so each new piece uses an idea you have already established.

Explain it to a willing partner unfamiliar with the process. Ask them what would happen in the ordinary case and then in the exception. If their answer exposes ambiguity, revise the explanation rather than adding every detail you know.

For a second version, assume an experienced listener. Remove the introductory layers they do not need and begin with the distinction relevant to their question. The goal is not a single perfect explanation for everyone; it is a reliable way to choose the next useful layer.

## Source trail and connections

Source inspected for this chapter: [Vinh Giang session 011 transcript](../../raw-material/youtube/transcripts/vinh-giang-wave-1/clean/011-Sqh6rt1hN2A.txt), text lines 1–220 and 238–401. Calibration appears at 88–130; the workshop analogy at 165–216; the learning-stage explanation at 242–322; the recap at 365–386. Lines 221–237 were not inspected for this chapter. References are local text lines, not video timestamps, and no independent visual analysis is claimed.

This develops approach 14 in the [original inventory](../../analysis/transcript-backed-concrete-speaking-approaches.md) and supports the [clarity and anti-rambling curriculum](../../analysis/clarity-and-anti-rambling-curriculum.md). Pair it with [compression](06-compress-before-expand.md): choose the amount of information, then arrange that information so the listener can use it.
