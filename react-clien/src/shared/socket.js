import { io } from "socket.io-client";
const SOCKET_URL = window["SOCKET_URL"] || "ws://localhost:1234";
export const socket = io(SOCKET_URL, {
  transports: ["websocket"],
});
socket.on("connect", () => {
  console.log("connected to server with id ", socket.id);
});
socket.onAny((eventName, ...args) => {
  console.debug(eventName, args);
});
export function joinRoom(roomId) {
  socket.emit("join_invite", roomId);
}
