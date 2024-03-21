import { DEFAULT_POSITION } from "chess.js";
import React from "react";

export default function useGame({
  myColor = "white",
  remainingTime = 20 * 60,
}) {
  const [fen, setFen] = React.useState(DEFAULT_POSITION);
  const [myRemainingTime, setMyRemainingTime] = React.useState(remainingTime);
  const [opponentRemainingTime, setOpponentRemainingTime] =
    React.useState(remainingTime);
  const isMyTurn = myColor.toLowerCase().startsWith(fen.split(" ")[1]);
  const intervalRef = React.useRef(null);
  React.useEffect(() => {
    clearInterval(intervalRef.current);
    intervalRef.current = setInterval(() => {
      if (isMyTurn) {
        setMyRemainingTime((prev) => prev - 1);
      } else {
        setOpponentRemainingTime((prev) => prev - 1);
      }
    }, 1000);
    return () => {
      clearInterval(intervalRef.current);
    };
  }, [isMyTurn]);
  return {
    fen,
    setFen,
    myRemainingTime,
    setMyRemainingTime,
    opponentRemainingTime,
    setOpponentRemainingTime,
    isMyTurn,
  };
}
