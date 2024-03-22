import { DEFAULT_POSITION } from "chess.js";
import React from "react";

export default function useGame({ remainingTime = 20 * 60 }) {
  const [fen, setFen] = React.useState(DEFAULT_POSITION);
  const [isGamePending, setIsGamePending] = React.useState(false);
  const [myRemainingTime, setMyRemainingTime] = React.useState(remainingTime);
  const [opponentRemainingTime, setOpponentRemainingTime] =
    React.useState(remainingTime);
  const [myColor, setMyColor] = React.useState("white");
  const isMyTurn = myColor.toLowerCase().startsWith(fen.split(" ")[1]);
  const intervalRef = React.useRef(null);
  React.useEffect(() => {
    if (isGamePending) {
      if (isMyTurn) {
        intervalRef.current = setInterval(() => {
          setMyRemainingTime((prev) => prev - 1);
        }, 1000);
      } else {
        intervalRef.current = setInterval(() => {
          setOpponentRemainingTime((prev) => prev - 1);
        }, 1000);
      }
    } else {
      clearInterval(intervalRef.current);
    }
    return () => {
      clearInterval(intervalRef.current);
    };
  }, [isMyTurn, isGamePending]);
  return {
    fen,
    setFen,
    myRemainingTime,
    setMyRemainingTime,
    opponentRemainingTime,
    setOpponentRemainingTime,
    isMyTurn,
    isGamePending,
    setIsGamePending,
    setMyColor,
    myColor,
  };
}
