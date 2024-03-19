import { create } from "zustand";


export const useRoomStore = create((set) => ({
  room_id: null,
  player_1: null,
  player_2: null,
  am_i_white: true,

  setRoomId: (id) => set({ room_id: id }),
  setPlayer1: (player) => set({ player_1: player }),
  setPlayer2: (player) => set({ player_2: player }),
  setAmIWhite: (am_i_white) => set({ am_i_white }),
  leaveRoom: () => set({ room_id: null, player_1: null, player_2: null }),
}));
