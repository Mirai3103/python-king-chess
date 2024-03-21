import { createRootRoute, Outlet } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/router-devtools";
import {chakra} from "@chakra-ui/react";
export const Route = createRootRoute({
  component: () => (
    <chakra.main textColor={'white'} bg={'gray.800'} h={'100vh'} w={'100vw'}>
      <Outlet />
      <TanStackRouterDevtools />
    </chakra.main>
  ),
});
