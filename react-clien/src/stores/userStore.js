import { create } from "zustand";



export const useUserStore = create((set) => ({
  user_id: null,
  display_name: null,
  setUserId: (id) => set({ user_id: id }),
  setDisplayName: (name) => set({ display_name: name }),
}));
