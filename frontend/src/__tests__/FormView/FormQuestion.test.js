import React from "react";
import Enzyme, { mount } from "enzyme";
import Adapter from "enzyme-adapter-react-16";

describe("formQuestionTests", () => {
  beforeAll(() => {
    Enzyme.configure({ adapter: new Adapter() });
  });

  it("renders a normal (no subquestions) multiple choice question correctly", () => {});

  it("renders a normal (no subquestions) short answer question correctly", () => {});
});
