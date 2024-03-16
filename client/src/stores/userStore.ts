import { create } from "zustand";

type UserStore = {
  user_id: string | null;
  display_name: string | null;
  setUserId: (id: string) => void;
  setDisplayName: (name: string) => void;
};

export const useUserStore = create<UserStore>((set) => ({
  user_id: null,
  display_name: null,
  setUserId: (id: string) => set({ user_id: id }),
  setDisplayName: (name: string) => set({ display_name: name }),
}));
