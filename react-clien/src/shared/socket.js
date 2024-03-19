import { io } from "socket.io-client";

export const socket = io("ws://127.0.0.1:1234", {
  transports: ["websocket"],
});
socket.on("connect", () => {
  console.log("connected to server with id ", socket.id);
});
socket.onAny((eventName, ...args) => {
  console.log(eventName, args);
});
