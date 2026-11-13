# Supply Chain Jenga — interface guide

## Design intent

A dependency atlas with a day scrubber. The primary task owns the largest part of the screen. Controls, evidence and measurements stay next to that task.

## Working interactions

1. Selectable suppliers and shared product dependencies.
2. Outage length, start, backup capacity and replenishment policy controls.
3. Scrub actual zero-based model days to inspect stocks and backlog.
4. Demand, fulfilment and inventory charts plus policy evaluations.

## Navigation and inputs

Workspace, experiment journal and About are available in the desktop rail and phone navigation. Guide explains this project. Reset restores this app’s sample state; Export downloads its state and results; Evaluate runs the implemented benchmark or invariants.

Use Tab to reach controls. Enter activates buttons. Draggable graph nodes support arrow-key movement and Enter selection. Space toggles supported live simulations when focus is outside a form. Esc closes the guide and pauses simulation. Touch supports the spatial canvases. Reduced-motion preferences suppress decorative animation.

## Responsive behaviour

Desktop workspaces prioritize the scene or editor. On narrow screens, inspectors stack below it; tables, source tabs, resident strips and graph canvases scroll inside their own containers. Graphs retain readable node sizes. The phone-width check used a 390px iframe with a measured 375px content viewport after its scrollbar. Actual mobile device/browser testing was not performed.

## State and evidence

The Python engine owns domain state and validates actions. Graph layout, selected evidence, gallery filters and temporary comparison slots are client interface state. Node dragging never silently changes the authored experiment protocol. Long computations run as cancellable local background jobs.

## Scope

Every shown value comes from the 75-day simulation under declared synthetic assumptions.

See MODEL_CARD.md for domain limits and DEMO.md for the exact walkthrough format.
