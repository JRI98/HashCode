function chooseContributors({ roles }, contributors) {
  let res = [];
  Object.entries(roles).forEach(([role, levelReq]) => {
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

    res.push(bestWorseContributor);
  });

  return res;
}
