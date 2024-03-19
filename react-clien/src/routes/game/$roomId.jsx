/* eslint-disable @typescript-eslint/no-explicit-any */
import {  createFileRoute,  } from "@tanstack/react-router";

import React from "react";
import axios from "axios";

import Game from "../../components/game";
import GameNotFound from "../../components/game_not_found";
import RoomFull from "../../components/room_full";
export const Route = createFileRoute("/game/$roomId")({
  component: Index,
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
function Index() {
  const { data } = Route.useLoaderData() 
  if (data.isNotFound) {
    return <GameNotFound />;
  }
  if (data.isRoomFull) {
    return <RoomFull />;
  }
  return <Game data={data} />;
}


