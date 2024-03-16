import { create } from "zustand";

type RoomStore = {
  room_id: string | null;
  player_1: string | null;
  player_2: string | null;
  am_i_white: boolean;

  setRoomId: (id: string) => void;
  setPlayer1: (player: string) => void;
  setPlayer2: (player: string) => void;
  setAmIWhite: (am_i_white: boolean) => void;
  leaveRoom: () => void;
};

export const useRoomStore = create<RoomStore>((set) => ({
  room_id: null,
  player_1: null,
  player_2: null,
  am_i_white: true,

  setRoomId: (id: string) => set({ room_id: id }),
  setPlayer1: (player: string) => set({ player_1: player }),
  setPlayer2: (player: string) => set({ player_2: player }),
  setAmIWhite: (am_i_white: boolean) => set({ am_i_white }),
  leaveRoom: () => set({ room_id: null, player_1: null, player_2: null }),
}));
