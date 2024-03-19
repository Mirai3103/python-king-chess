import { useNavigate } from "@tanstack/react-router";
import React from "react";
import { socket } from "../shared/socket";
import {Grid,Flex,Button,useToast} from "@chakra-ui/react";
import { Chessboard } from "react-chessboard";
import { DEFAULT_POSITION } from "chess.js";


export default function Game({data}) {
    const [fen, setFen] = React.useState(DEFAULT_POSITION);
    const amIWhite = data?.room?.white_id == socket.id;
    const isMyTurn = amIWhite ? fen.split(" ")[1] == "w" : fen.split(" ")[1] == "b";
    const toast = useToast();
    const navigate = useNavigate();
    React.useEffect(() => {
      if (data?.room?.player_1 != socket.id) {
        data?.room &&
          socket.emit("join_invite", data?.room?.id, (data) => {
            console.log("joined", data);
          });
      }
      function onMove(data) {
        console.log("moved", data);
       let checked = data.checked;
        if(checked){
            toast({
                colorScheme: "red",
                title: "Check",
                description: `${checked} is checked`,
                duration: 2000,
                isClosable: true,
            });
            }
        setFen(data.board);
        toast({
          colorScheme: "teal",
          title: "Moved",
          description: "Opponent moved",
          duration: 2000,
          isClosable: true,
        });
      }
      function onJoin(data) {
        console.log("joined", data);
        toast({
          colorScheme: "teal",
          title: "Joined",
          description: "Opponent joined",
          duration: 2000,
          isClosable: true,
        });
      }
  
      function onStarted(data) {
        const { white_id, fen } = data;
        setFen(fen);
        toast({
          colorScheme: "teal",
          title: "Started",
          description: white_id == socket.id ? "You are white" : "You are black",
          duration: 10000,
          isClosable: true,
        });
      }
      function onOpponentLeft(data) {
        console.log("opponent left", data);
        toast({
          colorScheme: "red",
          title: "Opponent left",
          description: "Opponent left the game",
          duration: 10000,
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
            socket.emit("move", payload, (data) => {
                if(data.is_error)
                {
                    toast({
                        title: "Lỗi",
                        description: data.message,
                        status: "error",
                        duration: 5000,
                        isClosable: true,
                        colorScheme: "red",
                      });
                }
            });
            return true;
          }}
          position={fen}
        />
      </Flex>
    );
  }
  
  
  