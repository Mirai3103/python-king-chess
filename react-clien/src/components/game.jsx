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
//import { useHistory } from "react-router-dom";

export default function Game({ data }) {
  const gameState = useGame({});
  const [roomData, setRoomData] = React.useState(data.room);
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
        <Flex
        key={index}
        justifyContent={
          msg.sender === socket.id ? "flex-end" : "flex-start"
        }
      >
        <chakra.span
          bg={msg.sender === socket.id ? "blue.500" : "gray.200"}
          p={"2"}
          borderRadius={"5px"}
          color={msg.sender === socket.id ? "white" : "black"}
        >
          {msg.message}
        </chakra.span>
      </Flex>
      ));
    } else {
      return <p>No messages</p>;
    }
  };
  const messageEl = renderMessages();
function leaveRoom() {
  const room_id = data.room.id;
  socket.emit("leave_room", { room_id }, (data) => {
      if (!data.is_error) {
          navigate("/");
      } else {
          toast({
              title: "Error",
              description: data.message,
              status: "error",
              duration: 5000,
              isClosable: true,
              colorScheme: "red",
          });
      }
  });
}

  const surrenderGame = () => {
    const confirmSurrender = window.confirm("Are you sure you want to surrender?");
    if (confirmSurrender) {
      const room_id = data.room.id;
      socket.emit("surrender", { room_id }, (data) => {
        if (data.is_error) {
          toast({
            title: "Error",
            description: data.message,
            status: "error",
            duration: 5000,
            isClosable: true,
            colorScheme: "red",
          });
        } else {
          navigate("/");
        }
      });
    }
  };
  //over
  const [gameStopped, setGameStopped] = React.useState(false);
  React.useEffect(() => {
    socket.on("stop_game", () => {
      setGameStopped(true);
    });
    return () => {
      socket.off("stop_game");
    };
  }, []);
  //over
  const rootBoardRef = React.useRef(null);
  const [boardWidth, setBoardWidth] = React.useState(400);
  const toast = useToast();
  const navigate = useNavigate();
  //const history = useHistory();
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
      socket.emit("get_current_room", (data) => {
        console.log("get_current_room", data);
        setRoomData(data.data);
      });
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
        description: white_id == socket.id ? "You play white" : "You play black",
        duration: 10000,
        isClosable: true,
      });
    }
    function onOpponentLeft(data) {
      console.log("opponent left", data);
      toast({
        colorScheme: "red",
        title: "The opponent leaves the game",
        description: "The opponent has left the game",
        duration: 10000,
        isClosable: true,
      });
      navigate({
        to: "/",
      });
    }
    function onOver(data) {
      console.log(data.winner+"--over")
      gameState.setIsGamePending(false);
      let winner= data.winner === "white" ? 'Trắng' : 'Đen';
      let description;
      if (data.winner === "draw") {
        description = "Match Draw.";
      } else {
        description = `The game ends! ${winner} win.`;
      }
      toast({
        colorScheme: "red",
        title: "Game over",
        description: description,
        duration: 10000,
        isClosable: true,
     
      });
      setTimeout(() => {
        const confirmQuit = window.confirm("Do you want to return to the home page?");
        if (confirmQuit) {
        window.location.href = "/";
        }
      }, 10000);
    }
    function onCheck(data) {
      const mycolor = gameState.myColor;
      console.log("checked", data.color, mycolor);
      if (mycolor.trim()===data.color.trim()) {
        toast({
          colorScheme: "red",
          title: "Chiếu",
          description: "You are checkmate",
          duration: 5000,
          isClosable: true,
        });
      } else {
        toast({
          colorScheme: "green",
          title: "Chiếu",
          description: "The opponent is checkmated",
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
    return () => {
      // gỡ bỏ các sự kiện socket
      socket.off("receive_message");
      socket.off("moved", onMove);
      socket.off("joined", onJoin);
      socket.off("game_started ", onStarted);
      socket.off("a_player_left", onOpponentLeft);
      socket.off("game_over", onOver);
      socket.off("checked", onCheck);
      socket.off("stop_game");
      socket.off("checked");
      socket.off("a_player_left");
    };
  }, [data, gameState, navigate]);

  function getOpponentName() {
    return socket.id == roomData?.player_1
      ? roomData?.player_2_name
      : roomData?.player_1_name;
  }
  function getMyName() {
    return socket.id == roomData?.player_1
      ? roomData?.player_1_name
      : roomData?.player_2_name;
  }
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
              {
               getOpponentName()||"Đối thủ"
              }
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
              //
              if (gameStopped) {
                return false;
              }
              //
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
                    title: "Error",
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
              {
                getMyName()||"Bạn"
              }
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
          <Button colorScheme="teal" size="sm" onClick={leaveRoom}>
            Rời phòng
          </Button>
          <Button colorScheme="teal" size="sm">
              Xin hòa
            </Button>
          <Button colorScheme="teal" size="sm" onClick={surrenderGame}>
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
              placeholder="Enter a message"
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
