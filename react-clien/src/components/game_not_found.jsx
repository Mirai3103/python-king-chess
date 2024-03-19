import {Grid,Flex,Button} from "@chakra-ui/react";
import {Link} from "@tanstack/react-router";
export default function GameNotFound() {
    return (
      <Grid placeContent={"center"} placeItems={"center"}>
        <Flex direction={"column"}>
          <h1>Game not found</h1>
          <Button colorScheme="teal" size="lg" as={Link} to={"/"}>
            Back to home
          </Button>
        </Flex>
      </Grid>
    );
  }
  