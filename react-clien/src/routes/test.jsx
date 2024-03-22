import { createFileRoute } from "@tanstack/react-router";
import Game from "../components/game";

export const Route = createFileRoute("/test")({
  component: Game,
});
