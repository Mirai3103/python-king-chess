import React from "react";
import {
  Flex,
  Button,
  chakra,
  Tag,
  Divider,
  Input,
  useToast,
} from "@chakra-ui/react";
import { Chessboard } from "react-chessboard";
import { DEFAULT_POSITION } from "chess.js";
import useGame from "../hooks/useGame";
import { useNavigate } from "@tanstack/react-router";
import { joinRoom, socket } from "../shared/socket";

export default function Game({ data }) {
  const gameState = useGame({});
  //
  const sendMessage = () => {
    const messageInput = document.getElementById("message-input");
    const message = messageInput.value.trim();
    if (message) {
      socket.emit("send_message", { message });
      messageInput.value = "";
    }
  };
  const renderMessages = () => {
    if (gameState.messages && gameState.messages.length > 0) {
      console.log(gameState.messages);
      let temp =[...gameState.messages]
      temp = temp.reverse();
      return temp
      .map((msg, index) => (
        <Flex key={index} justifyContent={msg.sender === socket.id ? "flex-end" : "flex-start"}>
          <chakra.span bg={"gray.700"} p={"2"} borderRadius={"5px"}>
            {msg.message}
          </chakra.span>
        </Flex>
      ));
    } else {
      return <p>No messages</p>;
    }
  };
  const messageEl = renderMessages();
  //
  const rootBoardRef = React.useRef(null);
  const [boardWidth, setBoardWidth] = React.useState(400);
  const toast = useToast();
  const navigate = useNavigate();
  React.useEffect(() => {
    if (rootBoardRef.current) {
      setBoardWidth(rootBoardRef.current.offsetHeight);
    }
  }, [rootBoardRef]);
  React.useEffect(() => {
    if (data?.room?.player_1 != socket.id) {
      data?.room && joinRoom(data.room.id);
    }
    function onMove(data) {
      console.log("moved", data);
      let checked = data.checked;
      if (checked) {
        toast({
          colorScheme: "red",
          title: "Check",
          description: `${checked} is checked`,
          duration: 2000,
          isClosable: true,
        });
      }
      gameState.setFen(data.room.fen);
      gameState.setMyRemainingTime(
        socket.id == data.room.player_1
          ? data.room.player_1_remaining_time
          : data.room.player_2_remaining_time
      );
      gameState.setOpponentRemainingTime(
        socket.id == data.room.player_1
          ? data.room.player_2_remaining_time
          : data.room.player_1_remaining_time
      );
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
      gameState.setMyColor(data.white_id == socket.id ? "white" : "black");
      const {
        white_id,
        fen,
        player_1_remaining_time,
        player_2_remaining_time,
      } = data;
      gameState.setMyRemainingTime(
        socket.id == data.player_1
          ? player_1_remaining_time
          : player_2_remaining_time
      );
      gameState.setOpponentRemainingTime(
        socket.id == data.player_1
          ? player_2_remaining_time
          : player_1_remaining_time
      );
      gameState.setFen(fen);
      gameState.setIsGamePending(true);
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
    // function onOver() {
    //   gameState.setIsGamePending(false);
    //   toast({
    //     colorScheme: "red",
    //     title: "Game over",
    //     description: "Game over",
    //     duration: 10000,
    //     isClosable: true,
    //   });
    //   navigate({
    //     to: "/",
    //   });
    // }
    function onOver(data) {
      gameState.setIsGamePending(false);
      let winner;
      if (data.winner === "white") {
        winner = "Đen";
      } else if (data.winner === "black") {
        winner = "Trắng";
      } else {
        winner = "Hòa";
      }
      toast({
        colorScheme: "red",
        title: "Kết thúc trò chơi",
        description: `Trò chơi kết thúc! ${winner} thắng.`,
        duration: 10000,
        isClosable: true,
      });
      navigate("/");
    }
    
    // if game.is_check(PieceColor.WHITE):
    //     await sio.emit("checked", room=room.id, data={"color": "white"})
    // if game.is_check(PieceColor.BLACK):
    //     await sio.emit("checked", room=room.id, data={"color": "black"})
    function onCheck(data) {
      const mycolor = gameState.myColor;
      if (data.color == mycolor) {
        toast({
          colorScheme: "red",
          title: "Chiếu",
          description: "Bạn bị chiếu tướng",
          duration: 5000,
          isClosable: true,
        });
      } else {
        toast({
          colorScheme: "red",
          title: "Chiếu",
          description: "Đối thủ bị chiếu tướng",
          duration: 5000,
          isClosable: true,
        });
      }
    }
    socket.on("receive_message", (data) => {
      console.log("receive_message", data);
      gameState.addMessage(data);
    });

    socket.on("checked", onCheck);
    socket.on("a_player_left", onOpponentLeft);
    socket.on("game_over", onOver);
    socket.on("a_player_joined", onJoin);
    socket.on("moved", onMove);
    socket.on("game_started", onStarted);
    //
    //
    return () => {
      socket.off("receive_message");
      socket.off("moved", onMove);
      socket.off("joined", onJoin);
      socket.off("game_started ", onStarted);
      socket.off("a_player_left", onOpponentLeft);
      socket.off("game_over", onOver);
      socket.off("checked", onCheck);
    };
  }, []);
  //
  
  //
  return (
    <Flex
      direction={"row"}
      height={"100vh"}
      w={"100vw"}
      gap={5}
      p={"10"}
      justifyContent={"center"}
      columnGap={"30px"}
    >
      <Flex direction={"column"} rowGap={"4"}>
        <Flex justifyContent={"space-between"} fontSize={"2xl"}>
          <h2>
            <chakra.span color={"red"}>
              Đối thủ
            </chakra.span>
          </h2>
          <Tag size="lg">
            {seccondsToTime(gameState.opponentRemainingTime || 0)}
          </Tag>
        </Flex>
        <chakra.div flexGrow={1} ref={rootBoardRef}>
          <Chessboard
            boardOrientation={gameState.myColor}
            boardWidth={boardWidth}
            position={gameState.fen || DEFAULT_POSITION}
            onPieceDrop={(from, to, piece) => {
              const mycolor = gameState.myColor;
              console.log(mycolor, piece);
              if (!piece.toLocaleLowerCase().startsWith(mycolor.charAt(0))) {
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
              if (gameState.fen.split(" ")[1] != mycolor.charAt(0)) {
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
              const payload = {
                move: { from, to, piece,
                  promotion: piece[1].toLowerCase() ?? "q"
                },
                room_id,
                remaining_time: gameState.myRemainingTime,
              };
              socket.emit("move", payload, (data) => {
                if (data.is_error) {
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
          />
        </chakra.div>
        <Flex justifyContent={"space-between"} fontSize={"2xl"}>
          <h2>
            <chakra.span color={"red"}>
              Bạn
            </chakra.span>
          </h2>
          <Tag size="lg">{seccondsToTime(gameState.myRemainingTime || 0)}</Tag>
        </Flex>
      </Flex>
      <Flex direction={"column"} basis={"300px"} bg={"gray.900"} p={"2"}>
        <Flex gap={"2"} wrap={"wrap"} w={"100%"}>
          <Button colorScheme="teal" size="sm"
          onClick={() => {
            navigator.clipboard.writeText(window.location.href);
          }}
          >
            Copy link
          </Button>
          <Button colorScheme="teal" size="sm" hidden>
            Rời phòng
          </Button>
          <Button colorScheme="teal" size="sm" hidden>
            Xin hòa
          </Button>
          <Button colorScheme="teal" size="sm" hidden>
            Đầu hàng
          </Button>
          <Button colorScheme="teal" size="sm" hidden>
            Xin hoàn nước
          </Button>
        </Flex>
        <Divider my={"4"} orientation="horizontal" />
        <chakra.h3 fontSize={"xl"}>Chat</chakra.h3>
        <Flex direction={"column-reverse"} flexGrow={1} gap={2} h={"100%"}>
          <Flex gap={1}>
            <Input
              id="message-input"
              placeholder="Nhập tin nhắn"
              bg={"gray.800"}
              color={"white"}
              p={"2"}
              w={"100%"}
              flexGrow={1}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  sendMessage();
                }
              }}
            />
            <Button colorScheme="teal" h={"100%"} px={"5"} size="sm" onClick={sendMessage}>
              Gửi
            </Button>
          </Flex>
          <Flex direction={"column-reverse"} flexGrow={1} gap={2} h={"100%"}>
          {messageEl}
          </Flex>
          {/* <Flex justifyContent={"flex-end"} w={"100%"}>
            <chakra.span bg={"gray.700"} p={"2"} borderRadius={"5px"}>
              Hello2
            </chakra.span>
          </Flex>
          <Flex justifyContent={"flex-start"} w={"100%"}>
            <chakra.span bg={"gray.700"} p={"2"} borderRadius={"5px"}>
              Hello
            </chakra.span> 
          </Flex> */}
        </Flex>
      </Flex>
    </Flex>
    //#endregion
    
    //#region
  );
}

function seccondsToTime(seconds) {
  let minutes = Math.floor(seconds / 60);
  let remainingSeconds = seconds % 60;
  if (minutes < 10) {
    minutes = "0" + minutes;
  }
  if (remainingSeconds < 10) {
    remainingSeconds = "0" + remainingSeconds;
  }
  return `${minutes}:${remainingSeconds}`;
}
