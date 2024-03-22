/* prettier-ignore-start */

/* eslint-disable */

// @ts-nocheck

// noinspection JSUnusedGlobalSymbols

// This file is auto-generated by TanStack Router

import { createFileRoute } from '@tanstack/react-router'

// Import Routes

import { Route as rootRoute } from './routes/__root'
import { Route as TestImport } from './routes/test'
import { Route as IndexImport } from './routes/index'
import { Route as GameIndexImport } from './routes/game/index'
import { Route as GameRoomIdImport } from './routes/game/$roomId'

// Create Virtual Routes

const AboutLazyImport = createFileRoute('/about')()

// Create/Update Routes

const AboutLazyRoute = AboutLazyImport.update({
  path: '/about',
  getParentRoute: () => rootRoute,
} as any).lazy(() => import('./routes/about.lazy').then((d) => d.Route))

const TestRoute = TestImport.update({
  path: '/test',
  getParentRoute: () => rootRoute,
} as any)

const IndexRoute = IndexImport.update({
  path: '/',
  getParentRoute: () => rootRoute,
} as any)

const GameIndexRoute = GameIndexImport.update({
  path: '/game/',
  getParentRoute: () => rootRoute,
} as any)

const GameRoomIdRoute = GameRoomIdImport.update({
  path: '/game/$roomId',
  getParentRoute: () => rootRoute,
} as any)

// Populate the FileRoutesByPath interface

declare module '@tanstack/react-router' {
  interface FileRoutesByPath {
    '/': {
      preLoaderRoute: typeof IndexImport
      parentRoute: typeof rootRoute
    }
    '/test': {
      preLoaderRoute: typeof TestImport
      parentRoute: typeof rootRoute
    }
    '/about': {
      preLoaderRoute: typeof AboutLazyImport
      parentRoute: typeof rootRoute
    }
    '/game/$roomId': {
      preLoaderRoute: typeof GameRoomIdImport
      parentRoute: typeof rootRoute
    }
    '/game/': {
      preLoaderRoute: typeof GameIndexImport
      parentRoute: typeof rootRoute
    }
  }
}

// Create and export the route tree

export const routeTree = rootRoute.addChildren([
  IndexRoute,
  TestRoute,
  AboutLazyRoute,
  GameRoomIdRoute,
  GameIndexRoute,
])

/* prettier-ignore-end */
