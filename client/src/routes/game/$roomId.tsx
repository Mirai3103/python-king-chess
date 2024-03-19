/* eslint-disable @typescript-eslint/no-explicit-any */
import { Link, createFileRoute, useNavigate } from "@tanstack/react-router";
import { Chessboard } from "react-chessboard";
import React from "react";
import axios from "axios";
import { Button, Flex, Grid } from "@chakra-ui/react";
import { socket } from "../../shared/socket";
import { useToast } from "@chakra-ui/react";
import { DEFAULT_POSITION } from "chess.js";
export const Route = createFileRoute("/game/$roomId")({
  component: Game,
  loader: async ({ params }) => {
    const roomId = params.roomId;
    const res = await axios.get(`http://localhost:1234/api/room/${roomId}`);
    const isError = res.data.is_error;
    console.log(res.data);
    return {
      data: {
        isRoomFull: res.data.data?.player_1 && res.data.data?.player_2,
        room: res.data.data?.room,
        isNotFound: isError,
      },
    };
  },
});
function Game() {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const { data } = Route.useLoaderData() as any;
  const [fen, setFen] = React.useState(DEFAULT_POSITION);
  const amIWhite = data?.room?.white_id == socket.id;
  const isMyTurn = amIWhite ? fen.split(" ")[1] == "w" : fen.split(" ")[1] == "b";
  const toast = useToast();
  const navigate = useNavigate();
  React.useEffect(() => {
    if (data?.room?.player_1 != socket.id) {
      data?.room &&
        socket.emit("join_invite", data?.room?.id, (data: any) => {
          console.log("joined", data);
        });
    }
    function onMove(data: any) {
      console.log("moved", data);
      setFen(data.board);
      toast({
        colorScheme: "teal",
        title: "Moved",
        description: "Opponent moved",
        duration: 2000,
        isClosable: true,
      });
    }
    function onJoin(data: any) {
      console.log("joined", data);
      toast({
        colorScheme: "teal",
        title: "Joined",
        description: "Opponent joined",
        duration: 2000,
        isClosable: true,
      });
    }

    function onStarted(data: any) {
      const { white_id, fen } = data;
      setFen(fen);
      toast({
        colorScheme: "teal",
        title: "Started",
        description: white_id == socket.id ? "You are white" : "You are black",
        duration: 2000,
        isClosable: true,
      });
    }
    function onOpponentLeft(data: any) {
      console.log("opponent left", data);
      toast({
        colorScheme: "red",
        title: "Opponent left",
        description: "Opponent left the game",
        duration: 2000,
        isClosable: true,
      });
      navigate({
        to: "/",
      });
    }
    socket.on("a_player_left", onOpponentLeft);

    socket.on("a_player_joined", onJoin);
    socket.on("moved", onMove);
    socket.on("game_started", onStarted);
    return () => {
      socket.off("moved", onMove);
      socket.off("joined", onJoin);
      socket.off("game_started ", onStarted);
      socket.off("a_player_left", onOpponentLeft);
    };
  }, []);
  if (data.isNotFound) {
    return <GameNotFound />;
  }
  if (data.isRoomFull) {
    return <RoomFull />;
  }
  console.log(data.room, socket.id);
  return (
    <Flex direction={"column"} gap={5}>
      <div>
        <span>
        Lượt của {isMyTurn ? "bạn" : "đối thủ"}
        </span>
      </div>
      <Chessboard
        boardOrientation={amIWhite ? "white" : "black"}
        boardWidth={500}
        id="BasicBoard"
        onPieceDrop={(from, to, piece) => {
          const mycolor = data.room.player_1 == socket.id ? "w" : "b";
          if (!piece.startsWith(mycolor)) {
            toast({
              title: "Invalid move",
              description: "It's not your piece",
              status: "error",
              duration: 2000,
              isClosable: true,
              colorScheme: "red",
            });
            return false;
          }
          if (fen.split(" ")[1] != mycolor) {
            toast({
              title: "Invalid move",
              description: "It's not your turn",
              status: "error",
              duration: 2000,
              isClosable: true,
              colorScheme: "red",
            });
            return false;
          }
          console.log(from, to, piece);
          const room_id = data.room.id;
          const payload = { move: { from, to, piece }, room_id };
          socket.emit("move", payload);
          return true;
        }}
        position={fen}
      />
    </Flex>
  );
}

function GameNotFound() {
  return (
    <Grid placeContent={"center"} placeItems={"center"}>
      <Flex direction={"column"}>
        <h1>Game not found</h1>
        <Button colorScheme="teal" size="lg" as={Link} to={"/"}>
          Back to home
        </Button>
      </Flex>
    </Grid>
  );
}

function RoomFull() {
  return (
    <Grid placeContent={"center"} placeItems={"center"}>
      <Flex direction={"column"}>
        <h1>Room is full</h1>
        <Button colorScheme="teal" size="lg" as={Link} to={"/"}>
          Back to home
        </Button>
      </Flex>
    </Grid>
  );
}
