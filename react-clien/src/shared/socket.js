import { io } from "socket.io-client";
const SOCKET_URL = process.env.SOCKET_URL || "ws://localhost:1234";
export const socket = io(SOCKET_URL, {
  transports: ["websocket"],
});
// {"state":{"user_id":null,"display_name":"Hoàng"},"version":0}
//user-storage
socket.on("connect", () => {
  console.log("connected to server with id ", socket.id);
  const state = JSON.parse(localStorage.getItem("user-storage")).state;
  console.log("state", state);
  if (state) {
    socket.emit("set_display_name", {
      name: state.display_name,
    });
    console.log("restored state", state);
  }
});
socket.onAny((eventName, ...args) => {
  console.debug(eventName, args);
});
export function joinRoom(roomId) {
  socket.emit("join_invite", roomId);
}
