import React, { useState, useEffect, useRef } from "react";
import { Flex, Button, chakra, Divider, useToast } from "@chakra-ui/react";
import { Chessboard } from "react-chessboard";
import { DEFAULT_POSITION } from "chess.js";
import { useNavigate } from "@tanstack/react-router";
import { socket } from "../shared/socket";

export default function GameWithBot({ data }) {
  const [fen, setFen] = useState(DEFAULT_POSITION);
  const rootBoardRef = useRef(null);
  const [boardWidth, setBoardWidth] = useState(400);
  const toast = useToast();
  const navigate = useNavigate();

  useEffect(() => {
    if (rootBoardRef.current) {
      setBoardWidth(rootBoardRef.current.offsetHeight);
    }
  }, [rootBoardRef]);

  useEffect(() => {
    const handleUpdateFen = (data) => {
      if (data.checked) {
        toast({
          title: "Check",
          description: "Bạn bị chiếu",
          status: "error",
          duration: 2000,
          isClosable: true,
          colorScheme: "red",
        });
      }

      // const { fromSquare, toSquare } = data;
      // setFen(data.fen);
      if(data && data.fen){
        setFen(data.fen);
      }
    };

    const handleGameOver = (data) => {
      let message;
      if (data.winner === 'white') message = "Bạn đã thắng";
      else if (data.winner === 'black') message = "Bạn đã thua";
      else message = "Hòa";
      setTimeout(() => {
        window.alert('Kết thúc trận đấu. Bạn sẽ được chuyển về trang chủ ');
        window.location.href = "/";
      }, 5000);
      toast({
        title: "Kết quả",
        description: message,
        status: "info",
        duration: 5000,
        isClosable: true,
        colorScheme: "blue",
      });

      // Đặt trạng thái fen thành null để ngăn trận đấu tiếp tục
      setFen(null);
    };

    socket.on("update_fen", handleUpdateFen);
    socket.on("game_over", handleGameOver);

    return () => {
      socket.off("update_fen", handleUpdateFen);
      socket.off("game_over", handleGameOver);
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
            <chakra.span color={"red"}>Stockfish</chakra.span>
          </h2>
        </Flex>
        <chakra.div flexGrow={1} ref={rootBoardRef}>
          <Chessboard
            boardOrientation={data.myColor}
            boardWidth={boardWidth}
            position={fen || DEFAULT_POSITION}
            onPieceDrop={(from, to, piece) => {
              // Thêm điều kiện kiểm tra fen khác null
              if (!fen) {
                return false;
              }

              const promotion = piece[1]?.toLowerCase() ?? "q";
              const mycolor = data.myColor;

              if (!piece.toLowerCase().startsWith(mycolor.charAt(0))) {
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

              if (fen.split(" ")[1] !== mycolor.charAt(0)) {
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
                move: { from, to, piece, promotion: promotion },
                fen: fen,
                promotion: promotion,
              };

              socket.emit("make_move_to_bot", payload, (data) => {
                if (data && data.is_error) {
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
            <chakra.span color={"red"}>Bạn</chakra.span>
          </h2>
        </Flex>
      </Flex>
      <Flex direction={"column"} basis={"300px"} bg={"gray.900"} p={"2"}>
        <Flex gap={"2"} wrap={"wrap"} w={"100%"}>
          <Button
            colorScheme="teal"
            size="sm"
            onClick={() => navigate("/")}
          >
            Quay lại trang chủ
          </Button>
        </Flex>
        <Divider my={"4"} orientation="horizontal" />
      </Flex>
    </Flex>
  );
}
