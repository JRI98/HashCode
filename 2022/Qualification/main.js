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

function getProjectScore(project, day) {
  const fullProject = projectsGlobal[project];
  const daysPastDue =
    day + fullProject.daysToCompletion - fullProject.bestBefore;
  return fullProject.score - Math.max(0, daysPastDue);
}

function readInput(lines) {
  let l = 0;
  const [nContributors, nProjects] = lines[l++]
    .split(" ")
    .map((s) => parseInt(s));
  const contributors = [];
  const projects = {};
  let projectNames = [];

  // Contributors
  while (true) {
    const [name, nSkills] = lines[l].split(" ");
    const skills = {};
    for (let i = 0; i < parseInt(nSkills); i++) {
      const [skill, level] = lines[l + i + 1].split(" ");
      skills[skill] = parseInt(level);
    }
    contributors.push({ name, skills, whenAvailable: 0 });
    l += parseInt(nSkills) + 1;

    if (Object.keys(contributors).length === nContributors) break;
  }

  // Projects
  while (true) {
    const [name, daysToCompletion, score, bestBefore, nRoles] =
      lines[l].split(" ");
    const roles = {};
    for (let i = 0; i < parseInt(nRoles); i++) {
      const [role, level] = lines[l + i + 1].split(" ");
      roles[role] = parseInt(level);
    }
    projects[name] = {
      daysToCompletion: parseInt(daysToCompletion),
      score: parseInt(score),
      bestBefore: parseInt(bestBefore),
      scorePerDay: parseInt(score) / parseInt(daysToCompletion),
      roles,
    };
    projectNames = Object.keys(projects);
    l += parseInt(nRoles) + 1;

    if (Object.keys(projects).length === nProjects) break;
  }

  return { contributors, projects, projectNames };
}

function isProjectPossible(project, contributors, day) {
  const fullProject = projectsGlobal[project];
  if (getProjectScore(project, day) <= 0) return false;

  let c = Object.entries(contributors);

  for (const [skill, level] of Object.entries(fullProject.roles)) {
    const contributorIdx = c.findIndex(
      (roles) => roles[1].skills[skill] >= level
    );
    if (contributorIdx !== -1) {
      c = [...c.slice(0, contributorIdx), ...c.slice(contributorIdx + 1)];
    } else {
      return false;
    }
  }

  return true;
}

function chooseContributors(project, contributors) {
  const fullProject = projectsGlobal[project];
  let res = [];
  Object.entries(fullProject.roles).forEach(([role, levelReq]) => {
    let bestWorseContributor;
    contributors.forEach((contributor) => {
      if (contributor.skills[role] >= levelReq) {
        if (
          !bestWorseContributor ||
          bestWorseContributor.skills[role] > contributor.skills[role]
        ) {
          bestWorseContributor = contributor;
        }
      }
    });

    res.push(bestWorseContributor.name);
  });

  return res;
}

// day: number
// projectsLeft: [name]
// availableContributors: [{name, skills: {skill: level}, whenAvailable: number}]
// Returns [[{name, contributors: [contributor]}], points]
function recursiveSearch(day, projectsLeft, allContributors) {
  // Check available contributors
  const availableContributors = allContributors.filter(
    (c) => c.whenAvailable <= day
  );

  // Filter out impossible choices
  const possibleProjects = [];
  for (const project of projectsLeft) {
    if (isProjectPossible(project, availableContributors, day)) {
      possibleProjects.push(project);
    }
  }

  // Break if there are no more projects available
  if (possibleProjects.length === 0) {
    if (availableContributors.length === allContributors.length) {
      return [[], 0];
    } else {
      return recursiveSearch(day + 1, projectsLeft, allContributors);
    }
  }

  // Iterate all projects that are possible
  let bestProject = null;
  let bestContributors = [];
  let bestOrder = [];
  let bestScore = 0;
  for (const project of possibleProjects) {
    // Deep copy the array
    const newAllContributors = allContributors.map((x) => ({
      ...x,
    }));

    let contributors = chooseContributors(project, availableContributors);
    newAllContributors.forEach((c) => {
      if (contributors.includes(c.name)) {
        c.whenAvailable = day + projectsGlobal[project].daysToCompletion;
      }
    });

    const [order, score] = recursiveSearch(
      day,
      projectsLeft.filter((p) => p !== project),
      newAllContributors
    );
    if (getProjectScore(project, day) + score > bestScore) {
      bestProject = project;
      bestContributors = contributors;
      bestOrder = order;
      bestScore = score;
    }
  }

  if (!bestProject) {
    return [[], 0];
  }

  return [
    [{ name: bestProject, contributors: bestContributors }, ...bestOrder],
    getProjectScore(bestProject, day) + bestScore,
  ];
}

let projectsGlobal = [];

async function main() {
  // Parse input
  const lines = await readLines();
  const input = readInput(lines);
  const contributors = input.contributors;
  projectsGlobal = input.projects;
  const projectNames = input.projectNames;

  // Compute solution
  const step = 1;
  let finalOrder = [];
  for (let i = 0; i < projectNames.length / step; i++) {
    finalOrder = [
      ...finalOrder,
      ...recursiveSearch(
        0,
        projectNames.slice(i * step, (i + 1) * step),
        contributors.slice(0, 25)
      )[0],
    ];
  }

  // Log result
  console.log(finalOrder.length);
  for (const work of finalOrder) {
    console.log(work.name);
    console.log(work.contributors.join(" "));
  }
}

main();
