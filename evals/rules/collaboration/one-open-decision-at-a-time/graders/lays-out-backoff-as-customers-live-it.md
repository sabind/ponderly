---
type: llm
---

The reply is Claude's answer to a request to design a retry for an upload worker that today loses a failed upload, where the first of three open decisions is fixed or exponential backoff, uploads come in bursts of a few hundred in a minute after a customer imports a shoot, and the storage provider throttles the worker when it hammers it.

PASS if the reply lays out the backoff decision as the customer who imported a shoot lives it: under fixed backoff, what happens to that burst of uploads while the provider is throttling, such as retries keeping the throttling going and the customer's photos staying unuploaded or failing for longer; under exponential backoff, what the same customer sees, such as the burst easing off so the uploads get through, perhaps more slowly or with a longer wait for the last ones. It recommends one of the two and gives a reason in those same terms, before the question. Judge only this first decision; holding back the attempt count and the last-failure handling is expected and is not a failure.
FAIL if either option is described only by its mechanism, such as the backoff formula, a fixed interval, delays doubling on each attempt or jitter, with nothing about what the customer's uploads do in the burst; if the reply only repeats the request's facts about bursts and throttling without saying what each option does to them; if there is no recommendation or the recommendation gives no reason; or if the reply asks no question about the backoff shape.
