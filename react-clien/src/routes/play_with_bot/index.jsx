import { createFileRoute } from '@tanstack/react-router'
import { Chessboard } from 'react-chessboard'
import React from 'react'
import GameWithBot from '../../components/game_with_bot'
import { socket } from '../../shared/socket'
export const Route = createFileRoute('/play_with_bot/')({
    component: Index,
    loader: async () => {
        const searchParams = new URLSearchParams(window.location.search)
        const myColor = searchParams.get('color') || 'white'
        const difficulty = searchParams.get('difficulty') || '1'
        console.log('color', difficulty)
        socket.emit('set_difficulty', {
            difficulty:Number(difficulty)
        })
        return {
            data: {
                myColor,
                difficulty
            }
        }
    }
})

function Index() {
    const data = Route.useLoaderData()
    return <GameWithBot data={{
        myColor: data.data.myColor,
        difficulty: data.data.difficulty
    }} />
}