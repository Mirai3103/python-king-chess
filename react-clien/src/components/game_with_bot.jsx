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
import { useNavigate } from "@tanstack/react-router";
import {  socket } from "../shared/socket";

export default function GameWithBot({data}) {
  const [fen, setFen] = React.useState(DEFAULT_POSITION);
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
    socket.on("update_fen", (data) => {
     console.log(data);
      setFen(data.fen);
    });
    return () => {
      socket.off("update_fen");
    };

    }, []);
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
              Stockfish
            </chakra.span>
          </h2>
        </Flex>
        <chakra.div flexGrow={1} ref={rootBoardRef}>
          <Chessboard
            boardOrientation={data.myColor}
            boardWidth={boardWidth}
            position={fen || DEFAULT_POSITION}
            onPieceDrop={(from, to, piece) => {
              const mycolor = data.myColor;
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
              if (fen.split(" ")[1] != mycolor.charAt(0)) {
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
              const payload = {
                move: { from, to, piece },
                fen: fen,
              };
              socket.emit("make_move_to_bot", payload, (data) => {
                if (data&&data.is_error) {
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
            }}
          />
        </chakra.div>
        <Flex justifyContent={"space-between"} fontSize={"2xl"}>
          <h2>
            <chakra.span color={"red"}>
              Bạn
            </chakra.span>
          </h2>
        </Flex>
      </Flex>
      <Flex direction={"column"} basis={"300px"} bg={"gray.900"} p={"2"}>
        <Flex gap={"2"} wrap={"wrap"} w={"100%"}>
          <Button colorScheme="teal" size="sm" onClick={() => navigate("/")}>
            Quay lại trang chủ
          </Button>
        </Flex>
        <Divider my={"4"} orientation="horizontal" />
        {/* <chakra.h3 fontSize={"xl"}>Chat</chakra.h3>
        <Flex direction={"column-reverse"} flexGrow={1} gap={2} h={"100%"}>
          <Flex gap={1}>
            <Input
              placeholder="Nhập tin nhắn"
              bg={"gray.800"}
              color={"white"}
              p={"2"}
              w={"100%"}
              flexGrow={1}
            />
            <Button colorScheme="teal" h={"100%"} px={"5"} size="sm">
              Gửi
            </Button>
          </Flex>
          <Flex justifyContent={"flex-end"} w={"100%"}>
            <chakra.span bg={"gray.700"} p={"2"} borderRadius={"5px"}>
              Hello2
            </chakra.span>
          </Flex>
          <Flex justifyContent={"flex-start"} w={"100%"}>
            <chakra.span bg={"gray.700"} p={"2"} borderRadius={"5px"}>
              Hello
            </chakra.span>
          </Flex>
        </Flex> */}
      </Flex>
    </Flex>
  );
}

