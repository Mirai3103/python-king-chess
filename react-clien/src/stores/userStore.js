import { create } from "zustand";
import { persist, createJSONStorage } from 'zustand/middleware'


export const useUserStore = create(persist((set) => ({
  user_id: null,
  display_name: null,
  setUserId: (id) => set({ user_id: id }),
  setDisplayName: (name) => set({ display_name: name }),
}), {
  name: 'user-storage',
  storage:createJSONStorage(()=>localStorage)
}));
