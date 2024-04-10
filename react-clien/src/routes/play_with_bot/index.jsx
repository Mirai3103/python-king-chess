import { createFileRoute } from '@tanstack/react-router'
import { Chessboard } from 'react-chessboard'
import React from 'react'
import GameWithBot from '../../components/game_with_bot'
export const Route = createFileRoute('/play_with_bot/')({
    component: Index,
    loader: async () => {
        const searchParams = new URLSearchParams(window.location.search)
        const myColor = searchParams.get('color') || 'white'
        return {
            data: {
                myColor
            }
        }
    }
})

function Index() {
    const data = Route.useLoaderData()
    return <GameWithBot data={{
        myColor: data.data.myColor
    }} />
}