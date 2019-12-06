import React from "react";
import Enzyme, { mount } from "enzyme";
import Adapter from "enzyme-adapter-react-16";

import Login from "../../Components/Login/Login";

describe("Login tests", () => {
  beforeAll(() => {
    Enzyme.configure({ adapter: new Adapter() });
  });

  it("renders normal email input box when there is no input in email", () => {
    // Arrange
    const wrapper = mount(<Login />);

    // Act

    // Assert
    // console.log(wrapper.debug());
    expect(
      wrapper
        .find("#email")
        .first()
        .prop("error")
    ).toEqual(false);

    // Cleanup
    wrapper.unmount();
  });

  it("renders error email input box (with red outline) when there is invalid input in email", () => {
    // Arrange
    const wrapper = mount(<Login />);

    // Act
    wrapper
      .childAt(0)
      .instance()
      .handleChange("email", "foo");
    wrapper.update();

    // Assert
    expect(
      wrapper
        .find("#email")
        .first()
        .prop("error")
    ).toEqual(true);

    // Cleanup
    wrapper.unmount();
  });

  it("renders error message if input email is not validated", () => {
    // Arrange
    const wrapper = mount(<Login />);

    // Act
    const button = wrapper.find("#signIn").first();
    button.simulate("click");

    // Assert
    // console.log(wrapper.debug());
    expect(wrapper.find("#errorFormat").first()).toBeDefined();

    // Cleanup
    wrapper.unmount();
  });
});
