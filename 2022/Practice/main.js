const readline = require("readline");

const LOGGING = false;

async function readLines() {
  const lines = [];

  await new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin });

    rl.on("line", function (line) {
      lines.push(line);
    });

    rl.on("close", function () {
      resolve();
    });
  });

  return lines;
}

function getPoints(ingredients, clients) {
  let res = 0;
  for (const c of Object.values(clients)) {
    if ([...ingredients].some((i) => c.dislikes.has(i))) continue;
    if ([...c.likes].every((l) => ingredients.has(l))) res += 1;
  }
  return res;
}

function removeClient(client, clientInfo, ingredientInfo) {
  for (const like of clientInfo[client].likes) {
    ingredientInfo[like].likes.delete(client);
  }

  for (const dislike of clientInfo[client].dislikes) {
    ingredientInfo[dislike].dislikes.delete(client);
  }

  clientInfo[client].likes.clear();
  clientInfo[client].dislikes.clear();
}

function removeIngredient(ingredient, clientInfo, ingredientInfo) {
  for (const like of ingredientInfo[ingredient].likes) {
    clientInfo[like].likes.delete(ingredient);
  }

  for (const dislike of ingredientInfo[ingredient].dislikes) {
    clientInfo[dislike].dislikes.delete(ingredient);
  }

  delete ingredientInfo[ingredient];
}

function addToFinalIngredients(
  ingredient,
  finalIngredients,
  clientInfo,
  ingredientInfo
) {
  for (const dislike of ingredientInfo[ingredient].dislikes) {
    removeClient(dislike, clientInfo, ingredientInfo);
  }

  removeIngredient(ingredient, clientInfo, ingredientInfo);

  finalIngredients.add(ingredient);
}

function calculateInfluence(clientInfo, ingredientInfo, ingredient) {
  let res = 0;

  for (const like of ingredientInfo[ingredient].likes) {
    res += 1 / (clientInfo[like].likes.size + clientInfo[like].dislikes.size);
  }

  for (const dislike of ingredientInfo[ingredient].dislikes) {
    res -=
      1 / (clientInfo[dislike].likes.size + clientInfo[dislike].dislikes.size);
  }

  return res;
}

async function main() {
  const lines = await readLines();

  const finalPizzaIngredients = new Set(); // Final result

  const immutableClientInfo = {}; // clientId => { likes: Set(ingredientId), dislikes: Set(ingredientId) }

  const clientInfo = {}; // clientId => { likes: Set(ingredientId), dislikes: Set(ingredientId) }
  const ingredientInfo = {}; // ingredientId => { likes: Set(clientId), dislikes: Set(clientId) }

  // Generate the client and ingredient maps
  const actualLines = lines.slice(1);
  for (let i = 0; i < actualLines.length / 2; i++) {
    const [, ...likedIngredients] = actualLines[i * 2].split(" ");
    const [, ...dislikedIngredients] = actualLines[i * 2 + 1].split(" ");

    immutableClientInfo[i] = {
      likes: new Set(likedIngredients),
      dislikes: new Set(dislikedIngredients),
    };

    clientInfo[i] = {
      likes: new Set(likedIngredients),
      dislikes: new Set(dislikedIngredients),
    };

    likedIngredients.map((li) => {
      if (!ingredientInfo[li]) {
        ingredientInfo[li] = { likes: new Set(), dislikes: new Set() };
      }

      ingredientInfo[li].likes.add(i);
    });

    dislikedIngredients.map((li) => {
      if (!ingredientInfo[li]) {
        ingredientInfo[li] = { likes: new Set(), dislikes: new Set() };
      }

      ingredientInfo[li].dislikes.add(i);
    });
  }

  // Discard ingredients with 0 likes
  Object.keys(ingredientInfo).forEach((v) => {
    if (ingredientInfo[v].likes.size === 0) {
      removeIngredient(v, clientInfo, ingredientInfo);
    }
  });

  // Add ingredients with 0 dislikes
  Object.keys(ingredientInfo).forEach((v) => {
    if (ingredientInfo[v].dislikes.size === 0) {
      addToFinalIngredients(
        v,
        finalPizzaIngredients,
        clientInfo,
        ingredientInfo
      );
    }
  });

  while (true) {
    if (LOGGING) {
      console.log();
      console.log();
      console.log();
      console.log(clientInfo);
      console.log(ingredientInfo);
    }

    // Compute the result
    let bestIngredient = null;
    let bestInfluence = 0;
    for (const ingredient of Object.keys(ingredientInfo)) {
      const influence = calculateInfluence(
        clientInfo,
        ingredientInfo,
        ingredient
      );
      if (influence > bestInfluence) {
        bestIngredient = ingredient;
        bestInfluence = influence;
      }

      if (LOGGING) {
        console.log(ingredient, influence);
      }
    }

    if (!bestIngredient) {
      break;
    }

    addToFinalIngredients(
      bestIngredient,
      finalPizzaIngredients,
      clientInfo,
      ingredientInfo
    );
  }

  console.log(finalPizzaIngredients.size, [...finalPizzaIngredients].join(" "));

  console.log(getPoints(finalPizzaIngredients, immutableClientInfo));
}

main();
