/* eslint-disable @typescript-eslint/no-explicit-any */
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import {
  Button,
  Flex,
  Grid,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
  Stack,
  useDisclosure,
  chakra
} from "@chakra-ui/react";
import { socket } from "../shared/socket";
import { useRoomStore } from "../stores/roomStore";
import React from "react";
import { Radio, RadioGroup } from "@chakra-ui/react";
import { useUserStore } from "../stores/userStore";
import { Input } from '@chakra-ui/react'
export const Route = createFileRoute("/")({
  component: () => <Index />,
});

function Index() {
  const { setPlayer1, setRoomId } = useRoomStore();
  const [color, setColor] = React.useState("white");
  const { isOpen, onOpen, onClose } = useDisclosure();
  const { setDisplayName, display_name } = useUserStore()
  const { isOpen:isOpenUserModal, onOpen: onOpenUserModal, onClose: onCloseUserModal } = useDisclosure();
  const navigate = useNavigate();
  const inputRef = React.useRef(null);
  function createRoom() {
    socket.emit(
      "create_invite",
      {
        am_i_white: color === "white",
      },
      (data) => {
        console.log("created room", data.data["room_id"]);
        setRoomId(data.data["room_id"]);
        setPlayer1(socket.id);
        navigate({
          to: `/game/$roomId`,
          params: { roomId: data.data["room_id"] },
        });
      }
    );
  }
  return (
    <Grid
      placeContent={"center"}
      placeItems={"center"}
      minW={"100vw"}
      minH={"100vh"}
    >
      <Flex direction={"column"} gap={5} maxW={"400px"} minW={'300px'}>
        <chakra.h1 fontSize="3xl" textAlign={'center'}>
          Chào {display_name||" Bạn"}
        </chakra.h1>
        <Button colorScheme="teal" size="lg" onClick={() => {
          navigate({to: '/play_with_bot',search: {color: 'white'}});
        }}>
          Chơi với máy
        </Button>
        <Button colorScheme="teal" size="lg" onClick={onOpen}>
          Tạo phòng
        </Button>
        <Button colorScheme="teal" size="lg" hidden>
          Tham gia phòng
        </Button>
        <Button colorScheme="teal" size="lg" onClick={onOpenUserModal} >
          Thông tin người chơi
        </Button>
      </Flex>
      <Modal isOpen={isOpenUserModal} onClose={onCloseUserModal}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>
            Thông tin người chơi
          </ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Input placeholder="Nhập tên của bạn" ref={inputRef} defaultValue={display_name} />
          </ModalBody>

          <ModalFooter>
            <Button colorScheme='blue' mr={3} onClick={() => {
              setDisplayName(inputRef.current.value)
              socket.emit('set_display_name', {
                name: inputRef.current.value
              })
              onCloseUserModal()
            }}>
              Lưu
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Modal Title</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <RadioGroup onChange={setColor} value={color}>
              <Stack direction="column">
                <Radio value="white">Trắng</Radio>
                <Radio value="black">Đen</Radio>
              </Stack>
            </RadioGroup>
          </ModalBody>

          <ModalFooter>
            <Button colorScheme="blue" mr={3} onClick={createRoom}>
              Tạo phòng
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
      
    </Grid>
  );
}
