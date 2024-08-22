function arrayDeepCopy(array) {
  return array.map((x) => ({ ...x }));
}
